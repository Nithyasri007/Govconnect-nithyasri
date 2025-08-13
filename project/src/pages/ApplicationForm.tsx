import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Upload, CheckCircle, AlertCircle, FileText, Mail } from 'lucide-react';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { apiService } from '../services/api';
import { Scheme } from '../types';

export const ApplicationForm: React.FC = () => {
  const { schemeId } = useParams<{ schemeId: string }>();
  const navigate = useNavigate();
  const [scheme, setScheme] = useState<Scheme | null>(null);
  const [userProfile, setUserProfile] = useState<any>(null);
  const [uploadedFiles, setUploadedFiles] = useState<{ [key: string]: File }>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [applicationSubmitted, setApplicationSubmitted] = useState(false);
  const [referenceNumber, setReferenceNumber] = useState('');

  useEffect(() => {
    // Load scheme details from backend
    const fetchScheme = async () => {
      if (!schemeId) {
        navigate('/schemes');
        return;
      }
      
      try {
        const fetchedScheme = await apiService.getScheme(schemeId);
        setScheme(fetchedScheme);
      } catch (error) {
        console.error('Error fetching scheme:', error);
        navigate('/schemes');
        return;
      }
    };

    fetchScheme();

    // Load user profile
    const extractedData = sessionStorage.getItem('govconnect_extracted_data');
    if (extractedData) {
      setUserProfile(JSON.parse(extractedData));
    }
  }, [schemeId, navigate]);

  const handleFileUpload = (documentType: string, file: File) => {
    setUploadedFiles(prev => ({
      ...prev,
      [documentType]: file
    }));
  };

  const handleSubmitApplication = async () => {
    if (!scheme || !userProfile) return;

    // Check if user is authenticated
    if (!apiService.isAuthenticated()) {
      // Store current path and redirect to auth
      sessionStorage.setItem('govconnect_redirect', window.location.pathname);
      navigate('/auth');
      return;
    }

    setIsSubmitting(true);

    try {
      const documents = Object.values(uploadedFiles);
      const result = await apiService.submitApplication(scheme.id, documents);
      setReferenceNumber(result.referenceNumber);
      setApplicationSubmitted(true);
    } catch (error) {
      console.error('Application submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!scheme) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <LoadingSpinner size="lg" className="mb-4" />
          <p className="text-gray-600">Loading scheme details...</p>
        </div>
      </div>
    );
  }

  if (applicationSubmitted) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="bg-green-50 border-b border-green-200 p-8 text-center">
            <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-green-900 mb-2">
              Application Submitted Successfully!
            </h1>
            <p className="text-green-700">
              Your application for {scheme.title} has been submitted.
            </p>
          </div>

          <div className="p-8">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
              <div className="flex items-center mb-3">
                <FileText className="w-6 h-6 text-blue-600 mr-2" />
                <h3 className="text-lg font-semibold text-blue-900">
                  Application Reference Number
                </h3>
              </div>
              <div className="text-2xl font-bold text-blue-600 bg-white px-4 py-2 rounded border-2 border-blue-300 text-center">
                {referenceNumber}
              </div>
              <p className="text-blue-700 mt-2 text-sm">
                Please save this reference number for future communication
              </p>
            </div>

            <div className="space-y-4 mb-6">
              <div className="flex items-start">
                <Mail className="w-5 h-5 text-green-600 mr-2 mt-0.5" />
                <div>
                  <p className="font-medium text-gray-900">Confirmation Email Sent</p>
                  <p className="text-sm text-gray-600">
                    A confirmation email has been sent to your registered email address with application details.
                  </p>
                </div>
              </div>

              <div className="flex items-start">
                <CheckCircle className="w-5 h-5 text-blue-600 mr-2 mt-0.5" />
                <div>
                  <p className="font-medium text-gray-900">Next Steps</p>
                  <p className="text-sm text-gray-600">
                    Your application will be reviewed by the concerned department. 
                    You will be notified about the status via SMS and email.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
              <div className="flex items-center mb-2">
                <AlertCircle className="w-5 h-5 text-yellow-600 mr-2" />
                <h4 className="font-semibold text-yellow-800">Important Notes:</h4>
              </div>
              <ul className="text-sm text-yellow-700 space-y-1">
                <li>• Keep your reference number safe for future reference</li>
                <li>• Processing time may vary from 15-30 working days</li>
                <li>• You may be contacted for additional documents if required</li>
                <li>• Track your application status using the reference number</li>
              </ul>
            </div>

            <div className="text-center space-y-4">
              <button
                onClick={() => navigate('/schemes')}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Explore More Schemes
              </button>
              
              <div>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(referenceNumber);
                  }}
                  className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                >
                  Copy Reference Number
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Apply for Scheme</h1>
        <h2 className="text-xl text-blue-600 font-semibold">{scheme.title}</h2>
        <p className="text-gray-600 mt-2">{scheme.department}</p>
      </div>

      <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
        {/* Scheme Summary */}
        <div className="bg-blue-50 border-b border-blue-200 p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">Scheme Benefits</h3>
          <p className="text-blue-800 font-medium">{scheme.benefits}</p>
        </div>

        <div className="p-8">
          {/* User Profile Confirmation */}
          {userProfile && (
            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Applicant Information
              </h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div><strong>Name:</strong> {userProfile.name}</div>
                  <div><strong>Date of Birth:</strong> {userProfile.dob}</div>
                  <div><strong>Gender:</strong> {userProfile.gender}</div>
                  <div><strong>Occupation:</strong> {userProfile.occupation || 'Not provided'}</div>
                  <div className="md:col-span-2">
                    <strong>Address:</strong> {userProfile.address || 'Not provided'}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Required Documents */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Required Documents
            </h3>
            <div className="space-y-4">
              {scheme.required_documents.map((document, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center">
                      <FileText className="w-5 h-5 text-blue-600 mr-2" />
                      <span className="font-medium text-gray-900">{document}</span>
                      <span className="text-red-500 ml-1">*</span>
                    </div>
                    {uploadedFiles[document] && (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    )}
                  </div>

                  {uploadedFiles[document] ? (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                      <div className="flex items-center justify-between">
                        <span className="text-green-800 font-medium">
                          {uploadedFiles[document].name}
                        </span>
                        <button
                          onClick={() => {
                            const newFiles = { ...uploadedFiles };
                            delete newFiles[document];
                            setUploadedFiles(newFiles);
                          }}
                          className="text-red-600 hover:text-red-700 text-sm"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  ) : (
                    <label className="block">
                      <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-400 transition-colors cursor-pointer">
                        <Upload className="w-6 h-6 text-gray-400 mx-auto mb-2" />
                        <span className="text-sm text-gray-600">
                          Click to upload {document}
                        </span>
                        <input
                          type="file"
                          accept=".jpg,.jpeg,.png,.pdf"
                          onChange={(e) => {
                            const file = e.target.files?.[0];
                            if (file) {
                              handleFileUpload(document, file);
                            }
                          }}
                          className="hidden"
                        />
                      </div>
                    </label>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Terms and Submit */}
          <div className="border-t border-gray-200 pt-6">
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
              <div className="flex items-start">
                <AlertCircle className="w-5 h-5 text-yellow-600 mr-2 mt-0.5" />
                <div className="text-sm text-yellow-800">
                  <p className="font-medium mb-1">Declaration:</p>
                  <p>
                    I hereby declare that the information provided is true and correct. 
                    I understand that providing false information may result in rejection 
                    of my application and legal consequences.
                  </p>
                </div>
              </div>
            </div>

            <div className="text-center">
              <button
                onClick={handleSubmitApplication}
                disabled={isSubmitting || scheme.required_documents.some(doc => !uploadedFiles[doc])}
                className="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors inline-flex items-center"
              >
                {isSubmitting ? (
                  <>
                    <LoadingSpinner size="sm" color="white" className="mr-2" />
                    Submitting Application...
                  </>
                ) : (
                  <>
                    <CheckCircle className="w-5 h-5 mr-2" />
                    Submit Application
                  </>
                )}
              </button>
              
              {scheme.required_documents.some(doc => !uploadedFiles[doc]) && (
                <p className="text-sm text-red-600 mt-2">
                  Please upload all required documents to proceed
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};