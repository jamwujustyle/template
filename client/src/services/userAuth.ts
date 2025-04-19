import { UserAuth } from "@/types/userAuth"
import api from "./api"
import { AxiosResponse } from "axios"
import { UserProfile, AuthTokens, PasswordResetRequest, PasswordResetConfirm } from "@/types/userAuth"

const userAuth = {
    userRegister: async (data: UserAuth): Promise<AxiosResponse<AuthTokens>> => {
        return await api.post('/auth/register', data);
    },
    userLogin: async (data: UserAuth): Promise<AxiosResponse<AuthTokens>> => {
    return await api.post('/auth/login', data)
    },
    getUserProfile: async (): Promise<AxiosResponse<UserProfile>> => {
        return await api.get('/auth/profile')
    },
    requestPasswordReset: async (data: PasswordResetRequest): Promise<AxiosResponse<{ msg: string }>> => {
        return await api.post('/auth/recover', data)
    },
    confirmPasswordReset: async (data: PasswordResetConfirm): Promise<AxiosResponse<{ msg: string }>> => {
        return await api.post('/auth/recover-confirm', data)
    }

}

export default userAuth

