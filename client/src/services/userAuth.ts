import { UserAuth } from "@/types/userAuth"
import api from "./api"

const userAuth = {
    userRegister: async (data: UserAuth) => {
        return await api.post('/register', data);
    },
    userLogin: async (data: UserAuth) => {
    return await api.post('/login', data)
        }
    // userRecover: (data:)
}

export default userAuth