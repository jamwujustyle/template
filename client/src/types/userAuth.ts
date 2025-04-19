export interface UserAuth {
  email: string;
  password: string;
}

export interface PasswordResetRequest {
  email: string;
}

export interface PasswordResetConfirm {
  token: string;
  password: string;
}

export interface UserProfile {
  id: string; // ?string or id?
  email: string;
}

export interface AuthTokens {
    access: string;
    refresh: string;
}
