"use client"; // Mark this component as a Client Component

import { useQuery, useMutation } from "@tanstack/react-query";
import userAuth from "@/services/userAuth";
import { UserAuth } from "@/types/userAuth";
import { AxiosResponse } from "axios";
import { useState } from "react";
const RegisterComponent = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const mutation = useMutation<AxiosResponse, Error, UserAuth>({
    mutationFn: (data: UserAuth) => userAuth.userRegister(data),
    onSuccess: (data) => {
      console.log("registration successful", data);
    },
    onError: (error: Error) => {
      console.error("error during registration: ", error);
    },
  });
  const handleRegister = () => {
    const userData: UserAuth = { email, password };
    mutation.mutate(userData);
  };

  return (
    <div>
      <h2>Register</h2>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleRegister();
        }}
      >
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={mutation.isPending}>
          Register
        </button>
      </form>

      {/* Display loading state */}
      {mutation.isPending && <p>Registering...</p>}
      {/* Display error message */}
      {mutation.error && <p>Error: {mutation.error.message}</p>}
    </div>
  );
};

export default RegisterComponent;
