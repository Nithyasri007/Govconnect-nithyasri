import { User, Scheme, Application, ExtractedData } from '../types';

// API service for connecting to FastAPI backend
class ApiService {
  private baseUrl = 'http://localhost:8000/api';
  private token: string | null = null;

  // Set authentication token
  setToken(token: string) {
    this.token = token;
    localStorage.setItem('govconnect_token', token);
  }

  // Get authentication token
  getToken(): string | null {
    if (!this.token) {
      this.token = localStorage.getItem('govconnect_token');
    }
    return this.token;
  }

  // Get headers for authenticated requests
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    
    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    return headers;
  }

  // Make HTTP request
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const config: RequestInit = {
      ...options,
      headers: this.getHeaders(),
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Authentication
  async signup(userData: Partial<User>): Promise<{ user: User; token: string }> {
    const response = await this.request<{ access_token: string; user: User }>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    
    this.setToken(response.access_token);
    localStorage.setItem('govconnect_user', JSON.stringify(response.user));
    
    return { user: response.user, token: response.access_token };
  }

  async login(email: string, password: string): Promise<{ user: User; token: string }> {
    const response = await this.request<{ access_token: string; user: User }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    this.setToken(response.access_token);
    localStorage.setItem('govconnect_user', JSON.stringify(response.user));
    
    return { user: response.user, token: response.access_token };
  }

  // OCR Document processing
  async uploadDocument(file: File): Promise<ExtractedData> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await this.request<{ extracted_data: ExtractedData }>('/documents/process', {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
    
    return response.extracted_data;
  }

  // Voice processing
  async uploadVoice(audioBlob: Blob): Promise<ExtractedData> {
    const formData = new FormData();
    formData.append('audio_file', audioBlob, 'voice_recording.wav');
    
    const response = await this.request<{ extracted_data: ExtractedData }>('/voice/process', {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
    
    return response.extracted_data;
  }

  // Scheme matching
  async getMatchingSchemes(userData: Partial<User>): Promise<Scheme[]> {
    const response = await this.request<{ schemes: Scheme[] }>('/schemes/match', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    
    return response.schemes;
  }

  // Get all schemes
  async getAllSchemes(): Promise<Scheme[]> {
    return await this.request<Scheme[]>('/schemes/');
  }

  // Get specific scheme
  async getScheme(schemeId: string): Promise<Scheme> {
    return await this.request<Scheme>(`/schemes/${schemeId}`);
  }

  // Application submission
  async submitApplication(schemeId: string, documents: File[]): Promise<{ referenceNumber: string }> {
    const response = await this.request<{ reference_number: string }>('/applications/', {
      method: 'POST',
      body: JSON.stringify({ scheme_id: parseInt(schemeId) }),
    });
    
    // Upload documents if provided
    if (documents.length > 0) {
      await this.uploadApplicationDocuments(response.reference_number, documents);
    }
    
    return { referenceNumber: response.reference_number };
  }

  // Upload application documents
  private async uploadApplicationDocuments(applicationId: string, documents: File[]): Promise<void> {
    for (const doc of documents) {
      const formData = new FormData();
      formData.append('file', doc);
      formData.append('document_type', 'supporting_document');
      
      await this.request(`/applications/${applicationId}/documents`, {
        method: 'POST',
        headers: {}, // Let browser set Content-Type for FormData
        body: formData,
      });
    }
  }

  // Get user applications
  async getUserApplications(): Promise<Application[]> {
    return await this.request<Application[]>('/applications/');
  }

  // Get user profile
  async getUserProfile(): Promise<User> {
    return await this.request<User>('/users/profile');
  }

  // Update user profile
  async updateUserProfile(userData: Partial<User>): Promise<User> {
    return await this.request<User>('/users/profile', {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  // Helper methods
  getCurrentUser(): User | null {
    const userStr = localStorage.getItem('govconnect_user');
    return userStr ? JSON.parse(userStr) : null;
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem('govconnect_user');
    localStorage.removeItem('govconnect_token');
  }
}

export const apiService = new ApiService();