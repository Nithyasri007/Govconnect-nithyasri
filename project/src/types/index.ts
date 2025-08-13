export interface User {
  id: number;
  name: string;
  email: string;
  dob?: string;
  gender?: string;
  occupation?: string;
  caste?: string;
  state?: string;
  phone?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Scheme {
  id: number;
  title: string;
  benefits: string;
  eligibility: {
    min_age?: number;
    max_age?: number;
    gender?: string[];
    occupation?: string[];
    caste?: string[];
    state?: string[];
    income_limit?: number;
  };
  required_documents: string[];
  department: string;
  description: string;
  application_process: string;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface Application {
  id: number;
  user_id: number;
  scheme_id: number;
  status: 'submitted' | 'under_review' | 'approved' | 'rejected';
  reference_number: string;
  created_at: string;
  updated_at: string;
  scheme?: Scheme;
  documents?: File[];
}

export interface ExtractedData {
  name?: string;
  dob?: string;
  gender?: string;
  address?: string;
  phone?: string;
  occupation?: string;
  caste?: string;
  state?: string;
  income?: number;
  [key: string]: string | number | undefined;
}