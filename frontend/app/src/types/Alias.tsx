export interface Alias {
  id: number;
  email: string;
  active: boolean;
  user_id: number;
  description?: string;
}

export interface AliasFormValues {
  active?: boolean;
  description?: string;
}
