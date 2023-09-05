export interface UsuarioBase {
  username: string;
  recipient_email: string;
  password: string;
  remember_token: string;
}

export interface UsuarioCreate extends UsuarioBase {}

export interface Usuario extends UsuarioBase {
  id: number;
}