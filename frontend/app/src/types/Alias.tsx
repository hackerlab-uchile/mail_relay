export interface Alias {
    id: number;
    email: string;
    active: boolean;
    user_id: number;
}

export interface AliasFormValues {
    email: string;
    active?: boolean;
    comment?: string;
}