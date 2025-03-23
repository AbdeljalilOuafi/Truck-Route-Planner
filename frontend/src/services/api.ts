import axios from 'axios';
import { RouteInput } from '../types';

const API_BASE_URL = 'https://ouafi.tech/api';

export const calculateRoute = async (input: RouteInput) => {
  const response = await axios.post(`${API_BASE_URL}/calculate-route/`, input);
  return response.data;
};