import React from 'react';
import { Link } from 'react-router-dom';
import { Upload, Mic, FileText, Search, Shield, Clock } from 'lucide-react';

export const Home: React.FC = () => {
  const features = [
    {
      icon: Upload,
      title: 'Document Upload',
      description: 'Upload your Aadhaar, PAN, or other documents. Our OCR technology will extract your details automatically.',
      link: '/upload/document',
      color: 'bg-blue-500'
    },
    {
      icon: Mic,
      title: 'Voice Input',
      description: 'Simply speak your details and let our voice recognition technology capture your information.',
      link: '/upload/voice',
      color: 'bg-green-500'
    },
    {
      icon: FileText,
      title: 'Manual Form',
      description: 'Prefer to type? Fill in your details manually using our comprehensive form.',
      link: '/form/manual',
      color: 'bg-orange-500'
    }
  ];

  const benefits = [
    {
      icon: Search,
      title: 'Smart Matching',
      description: 'Advanced algorithms match you with eligible schemes based on your profile'
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your personal data is encrypted and protected with government-grade security'
    },
    {
      icon: Clock,
      title: 'Quick Processing',
      description: 'Get matched with schemes in minutes and track your applications in real-time'
    }
  ];

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center max-w-3xl mx-auto">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              Connect with
              <span className="block text-yellow-300">Government Schemes</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100 leading-relaxed">
              Discover and apply for welfare schemes through multiple input methods. 
              Upload documents, use voice input, or fill forms manually.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/schemes"
                className="bg-yellow-400 text-blue-900 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-yellow-300 transition-colors shadow-lg"
              >
                Browse All Schemes
              </Link>
              <Link
                to="/upload/document"
                className="bg-transparent border-2 border-white text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-white hover:text-blue-900 transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Input Methods Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Choose Your Preferred Input Method
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Multiple ways to provide your information for scheme eligibility checking
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="group">
                <Link
                  to={feature.link}
                  className="block bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-gray-100"
                >
                  <div className="p-8">
                    <div className={`w-16 h-16 ${feature.color} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                      <feature.icon className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-4">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose GovConnect?
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {benefits.map((benefit, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <benefit.icon className="w-8 h-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  {benefit.title}
                </h3>
                <p className="text-gray-600">
                  {benefit.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-blue-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl md:text-5xl font-bold text-yellow-300 mb-2">500+</div>
              <div className="text-blue-200">Government Schemes</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold text-yellow-300 mb-2">1M+</div>
              <div className="text-blue-200">Citizens Helped</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold text-yellow-300 mb-2">28</div>
              <div className="text-blue-200">States & UTs Covered</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
            Ready to Find Your Benefits?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Start your journey to accessing government welfare schemes today
          </p>
          <Link
            to="/upload/document"
            className="inline-flex items-center bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
          >
            <Upload className="w-5 h-5 mr-2" />
            Start with Document Upload
          </Link>
        </div>
      </section>
    </div>
  );
};