import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { CheckCircle, ExternalLink, ArrowRight, Award, FileText, Clock, AlertCircle } from 'lucide-react';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { apiService } from '../services/api';
import { Scheme } from '../types';

export const SchemeResults: React.FC = () => {
  const navigate = useNavigate();
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [loading, setLoading] = useState(true);
  const [userProfile, setUserProfile] = useState<any>(null);

  useEffect(() => {
    const loadSchemes = async () => {
      try {
        // Get user data from session storage
        const extractedData = sessionStorage.getItem('govconnect_extracted_data');
        if (!extractedData) {
          navigate('/');
          return;
        }

        const userData = JSON.parse(extractedData);
        setUserProfile(userData);

        // Get matching schemes
        const matchingSchemes = await apiService.getMatchingSchemes(userData);
        setSchemes(matchingSchemes);
      } catch (error) {
        console.error('Error loading schemes:', error);
      } finally {
        setLoading(false);
      }
    };

    loadSchemes();
  }, [navigate]);

  const calculateAge = (dob: string) => {
    if (!dob) return null;
    const birthDate = new Date(dob);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return age;
  };

  const getEligibilityScore = (scheme: Scheme) => {
    let score = 0;
    let totalCriteria = 0;

    const age = userProfile?.dob ? calculateAge(userProfile.dob) : null;

    // Age eligibility
    if (scheme.eligibility.min_age || scheme.eligibility.max_age) {
      totalCriteria++;
      if (age) {
        const minAge = scheme.eligibility.min_age || 0;
        const maxAge = scheme.eligibility.max_age || 100;
        if (age >= minAge && age <= maxAge) score++;
      }
    }

    // Gender eligibility
    if (scheme.eligibility.gender && scheme.eligibility.gender.length > 0) {
      totalCriteria++;
      if (userProfile?.gender && scheme.eligibility.gender.includes(userProfile.gender.toLowerCase())) {
        score++;
      }
    }

    // Occupation eligibility
    if (scheme.eligibility.occupation && scheme.eligibility.occupation.length > 0) {
      totalCriteria++;
      if (userProfile?.occupation) {
        const userOccupation = userProfile.occupation.toLowerCase();
        const matches = scheme.eligibility.occupation.some(occ => 
          userOccupation.includes(occ.toLowerCase())
        );
        if (matches) score++;
      }
    }

    return totalCriteria > 0 ? Math.round((score / totalCriteria) * 100) : 100;
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <LoadingSpinner size="lg" className="mb-4" />
          <p className="text-gray-600">Finding matching schemes for you...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center mb-4">
          <CheckCircle className="w-8 h-8 text-green-600 mr-3" />
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Matching Schemes Found</h1>
            <p className="text-lg text-gray-600">
              Based on your profile, here are the schemes you may be eligible for
            </p>
          </div>
        </div>

        {/* User Profile Summary */}
        {userProfile && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-blue-900 mb-2">Your Profile Summary:</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-blue-800">
              <div>
                <strong>Name:</strong> {userProfile.name || 'Not provided'}
              </div>
              <div>
                <strong>Age:</strong> {userProfile.dob ? `${calculateAge(userProfile.dob)} years` : 'Not provided'}
              </div>
              <div>
                <strong>Gender:</strong> {userProfile.gender || 'Not provided'}
              </div>
              <div>
                <strong>Occupation:</strong> {userProfile.occupation || 'Not provided'}
              </div>
              <div>
                <strong>State:</strong> {userProfile.state || 'Not provided'}
              </div>
              <div>
                <strong>Category:</strong> {userProfile.caste || 'Not provided'}
              </div>
            </div>
          </div>
        )}
      </div>

      {schemes.length === 0 ? (
        <div className="text-center py-12">
          <AlertCircle className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">No Matching Schemes Found</h2>
          <p className="text-gray-600 mb-6">
            We couldn't find schemes matching your current profile. Try updating your information or check back later.
          </p>
          <Link
            to="/"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Try Different Input Method
          </Link>
        </div>
      ) : (
        <>
          <div className="mb-6">
            <p className="text-gray-600">
              Found <strong className="text-blue-600">{schemes.length}</strong> schemes you may be eligible for
            </p>
          </div>

          {/* Schemes Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {schemes.map((scheme) => {
              const eligibilityScore = getEligibilityScore(scheme);
              
              return (
                <div key={scheme.id} className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-shadow">
                  {/* Header */}
                  <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center">
                        <Award className="w-6 h-6 mr-2" />
                        <span className="text-sm font-medium bg-blue-500 bg-opacity-50 px-2 py-1 rounded">
                          {scheme.department}
                        </span>
                      </div>
                      <div className="text-right">
                        <div className={`text-xs font-semibold px-2 py-1 rounded ${
                          eligibilityScore >= 80 ? 'bg-green-500' : 
                          eligibilityScore >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}>
                          {eligibilityScore}% Match
                        </div>
                      </div>
                    </div>
                    <h3 className="text-xl font-bold leading-tight">{scheme.title}</h3>
                  </div>

                  {/* Content */}
                  <div className="p-6">
                    {/* Benefits */}
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Benefits:</h4>
                      <p className="text-green-700 font-medium bg-green-50 p-3 rounded-lg">
                        {scheme.benefits}
                      </p>
                    </div>

                    {/* Description */}
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Description:</h4>
                      <p className="text-gray-600 text-sm leading-relaxed">
                        {scheme.description}
                      </p>
                    </div>

                    {/* Required Documents */}
                    <div className="mb-6">
                      <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                        <FileText className="w-4 h-4 mr-1" />
                        Required Documents:
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {scheme.required_documents.map((doc, index) => (
                          <span
                            key={index}
                            className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded border"
                          >
                            {doc}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Application Process */}
                    <div className="mb-6">
                      <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                        <Clock className="w-4 h-4 mr-1" />
                        How to Apply:
                      </h4>
                      <p className="text-sm text-gray-600">
                        {scheme.application_process}
                      </p>
                    </div>

                    {/* Action Button */}
                    <Link
                      to={`/application/${scheme.id}`}
                      className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center group"
                    >
                      Apply Now
                      <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Additional Actions */}
          <div className="mt-8 text-center">
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Need Help with Applications?
              </h3>
              <p className="text-gray-600 mb-4">
                Contact your nearest Common Service Centre (CSC) or District Collector's office for assistance.
              </p>
              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <Link
                  to="/"
                  className="bg-white border border-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Try Different Input Method
                </Link>
                <a
                  href="#"
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors inline-flex items-center"
                >
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Find Nearest CSC
                </a>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};