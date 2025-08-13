import { Scheme } from '../types';

export const schemes: Scheme[] = [
  {
    id: '1',
    title: 'Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)',
    benefits: 'Financial assistance of ₹6,000 per year to eligible farmer families',
    eligibility: {
      occupation: ['farmer', 'agriculture'],
      income_limit: 200000
    },
    required_documents: ['Aadhaar Card', 'Bank Account Details', 'Land Records'],
    department: 'Ministry of Agriculture & Farmers Welfare',
    description: 'PM-KISAN provides income support to landholding farmers\' families across the country to supplement their financial needs for procuring various inputs related to agriculture and allied activities as well as domestic needs.',
    application_process: 'Apply online through PM-KISAN portal or visit nearest Common Service Centre (CSC)'
  },
  {
    id: '2',
    title: 'Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (AB PM-JAY)',
    benefits: 'Health insurance coverage of ₹5 lakh per family per year',
    eligibility: {
      income_limit: 180000
    },
    required_documents: ['Aadhaar Card', 'Ration Card', 'Income Certificate'],
    department: 'Ministry of Health and Family Welfare',
    description: 'World\'s largest health insurance scheme providing cashless treatment at empaneled hospitals for secondary and tertiary care hospitalization.',
    application_process: 'Visit nearest empaneled hospital or Common Service Centre with required documents'
  },
  {
    id: '3',
    title: 'Pradhan Mantri Awas Yojana (PMAY)',
    benefits: 'Financial assistance for construction/purchase of houses',
    eligibility: {
      income_limit: 300000
    },
    required_documents: ['Aadhaar Card', 'Income Certificate', 'Property Documents'],
    department: 'Ministry of Housing and Urban Affairs',
    description: 'Housing for All mission aims to provide pucca houses with water connection, toilet, electricity and LPG connection to all eligible families.',
    application_process: 'Apply online through PMAY portal or visit nearest Urban Local Body office'
  },
  {
    id: '4',
    title: 'National Social Assistance Programme (NSAP)',
    benefits: 'Monthly pension for elderly, widows, and disabled persons',
    eligibility: {
      min_age: 60,
      income_limit: 120000
    },
    required_documents: ['Aadhaar Card', 'Age Proof', 'Income Certificate', 'Bank Account Details'],
    department: 'Ministry of Rural Development',
    description: 'NSAP represents a significant step towards the fulfillment of the Directive Principles in Article 41 of the Constitution.',
    application_process: 'Apply through respective State Government offices or online portals'
  },
  {
    id: '5',
    title: 'Pradhan Mantri Mudra Yojana (PMMY)',
    benefits: 'Collateral-free loans up to ₹10 lakh for micro enterprises',
    eligibility: {
      occupation: ['self-employed', 'entrepreneur', 'small business']
    },
    required_documents: ['Aadhaar Card', 'PAN Card', 'Business Plan', 'Bank Statements'],
    department: 'Ministry of Finance',
    description: 'MUDRA provides loans to micro/small business enterprises and to individuals who wish to start a business.',
    application_process: 'Apply through participating banks, NBFCs, or MFIs'
  },
  {
    id: '6',
    title: 'Beti Bachao Beti Padhao',
    benefits: 'Financial incentives and educational support for girl children',
    eligibility: {
      gender: ['female'],
      max_age: 18
    },
    required_documents: ['Birth Certificate', 'Aadhaar Card', 'School Enrollment Certificate'],
    department: 'Ministry of Women and Child Development',
    description: 'Initiative to generate awareness and improve the efficiency of welfare services for girls.',
    application_process: 'Apply through schools, Anganwadi centers, or district offices'
  }
];