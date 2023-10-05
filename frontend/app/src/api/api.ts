import { LoginCredentials, LoginResponse } from "@/hooks/auth";
import { Usuario, UsuarioCreate } from "@/types/Usuario";
import { Alias, AliasFormValues } from "@/types/Alias";
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

  export async function signupUser(signupData: UsuarioCreate): Promise<Usuario> {
    return apiClient
        .post("/users/signup/", signupData)
        .then((response) => response.data);
}

export async function getAliases() {
  try {
    const response = await apiClient.get<Alias[]>("/aliases/");
    return response.data;
  } catch (error: any) {
    if (error.response && error.response.status === 404) {
      return [];
    } else {
      throw error;
    }
  }
}

export async function updateAlias(aliasId: number, updatedAlias: Partial<Alias>): Promise<Alias> {
  return await apiClient
    .put<Alias>(`/aliases/${aliasId}`, updatedAlias)
    .then((response) => response.data);
}

export async function createAlias(alias: AliasFormValues) {
  return apiClient.post("/aliases/", alias).then((response) => response.data);
}

