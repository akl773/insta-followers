import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export interface User {
  id: string;
  username: string;
  full_name: string;
  profile_pic_url: string;
  type?: string[];
}

export interface Report {
  _id: string;
  generated_at: string;
  num_followers: number;
  num_following: number;
  users: User[];
  new_followers: string[];
  lost_followers: string[];
  new_following: string[];
  unfollowed: string[];
  stats: Record<string, any>;
}

export interface NotFollowingBackUser {
  username: string;
  full_name: string;
  profile_pic_url: string;
  instagram_url: string;
}

export interface UserDetails {
  id: string;
  username: string;
  full_name: string;
  profile_pic_url: string;
  biography: string;
  website: string;
  is_private: boolean;
  is_verified: boolean;
  followers_count: number;
  following_count: number;
  media_count: number;
}

export const apiService = {
  // User details
  getUserDetails: (username: string) => 
    api.get<{success: boolean; data: UserDetails}>(`/user/${username}`),
  getReports: (limit: number = 20) => {
    return api.get(`/reports?limit=${limit}`);
  },
  getLatestReport: () => api.get('/reports/latest'),
};

export default api;
