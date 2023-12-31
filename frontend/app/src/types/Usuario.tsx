export interface UsuarioBase {
  username: string;
  recipient_email: string;
  password: string;
  turnstile_response?: string;
}

export interface UsuarioCreate extends UsuarioBase {}

export interface Usuario extends UsuarioBase {
  id: number;
}
