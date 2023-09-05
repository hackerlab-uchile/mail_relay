import { LoginCredentials, LoginResponse } from "@/hooks/auth";
import { Usuario } from "@/types/Usuario";
import apiClient from "@/utils/axios";


export async function getUsuarioToken(
    credentials: LoginCredentials
  ): Promise<LoginResponse> {
    return apiClient
      .post<LoginResponse>(
        "/users/signin",
        {
          username: credentials.username,
          password: credentials.password,
        },
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      )
      .then((response) => response.data);
  }
  
  export async function getCurrentUsuario(): Promise<Usuario> {
    return await apiClient
      .get<Usuario>("/users/me")
      .then((response) => response.data);
  }