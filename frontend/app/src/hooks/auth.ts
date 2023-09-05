import { useMutation, useQuery } from "@tanstack/react-query";
import * as api from "@/api/api";

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export type LoginCredentials = {
  username: string;
  password: string;
};

export const login = (credentials: { username: string; password: string }) =>
  api
    .getUsuarioToken(credentials)
    .then((data) => {
      localStorage.setItem("token", data.access_token);
      return data;
    })
    .catch((err) => {
      localStorage.removeItem("token");
      throw err;
    });

export const logout = async () => {
  localStorage.removeItem("token");
};

export const useUser = () => {
  return useQuery({
    queryKey: ["usuario", "me"],
    queryFn: api.getCurrentUsuario,
    retry: false,
    enabled: typeof window !== "undefined",
  });
};