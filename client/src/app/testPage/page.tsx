"use client"; // Mark this component as a Client Component

import React, { useState } from "react"; // Import React if not already present
import { useMutation } from "@tanstack/react-query";
import { UserAuth } from "@/types/userAuth";
import userAuth from "@/services/userAuth";

const AuthTestPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  // Placeholder for state and handlers - you will implement these
  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await userAuth.userRegister({ email, password });
      setMessage();
    } catch (error) {
      console.error("error during registration ", error);
      setError(error.response?.data?.detail || "Registration failed");
    }
  };

  const handleLoginSubmit = (e: React.FormEvent) => e.preventDefault();
  const handleFetchProfile = () => {};
  const handleLogout = () => {};
  const handleRequestResetSubmit = (e: React.FormEvent) => e.preventDefault();
  const handleConfirmResetSubmit = (e: React.FormEvent) => e.preventDefault();

  return (
    <div
      style={{
        fontFamily: "sans-serif",
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        gap: "40px",
      }}
    >
      <h1>Auth Test Page</h1>

      {/* General Messages/Errors */}
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Registration Section */}
      <section
        style={{
          border: "1px solid #ccc",
          padding: "15px",
          borderRadius: "5px",
        }}
      >
        <h2>Register</h2>
        <form
          onSubmit={handleRegisterSubmit}
          style={{ display: "flex", flexDirection: "column", gap: "10px" }}
        >
          <div>
            <label htmlFor="register-email" style={{ marginRight: "5px" }}>
              Email:
            </label>
            <input
              type="email"
              id="register-email"
              // value={registerEmail}
              // onChange={(e) => setRegisterEmail(e.target.value)}
              required
              style={{
                padding: "8px",
                border: "1px solid #ccc",
                borderRadius: "3px",
              }}
            />
          </div>
          <div>
            <label htmlFor="register-password" style={{ marginRight: "5px" }}>
              Password:
            </label>
            <input
              type="password"
              id="register-password"
              // value={registerPassword}
              // onChange={(e) => setRegisterPassword(e.target.value)}
              required
              style={{
                padding: "8px",
                border: "1px solid #ccc",
                borderRadius: "3px",
              }}
            />
          </div>
          <button
            type="submit"
            style={{
              padding: "10px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "3px",
              cursor: "pointer",
            }}
          >
            Register
          </button>
          {/* Placeholder for loading/error specific to this form */}
        </form>
      </section>

      {/* Login/Profile Section */}
      <section
        style={{
          border: "1px solid #ccc",
          padding: "15px",
          borderRadius: "5px",
        }}
      >
        <h2>Login / Profile</h2>
        {!userIsLoggedIn ? (
          <form
            onSubmit={handleLoginSubmit}
            style={{ display: "flex", flexDirection: "column", gap: "10px" }}
          >
            <div>
              <label htmlFor="login-email" style={{ marginRight: "5px" }}>
                Email:
              </label>
              <input
                type="email"
                id="login-email"
                // value={loginEmail}
                // onChange={(e) => setLoginEmail(e.target.value)}
                required
                style={{
                  padding: "8px",
                  border: "1px solid #ccc",
                  borderRadius: "3px",
                }}
              />
            </div>
            <div>
              <label htmlFor="login-password" style={{ marginRight: "5px" }}>
                Password:
              </label>
              <input
                type="password"
                id="login-password"
                // value={loginPassword}
                // onChange={(e) => setLoginPassword(e.target.value)}
                required
                style={{
                  padding: "8px",
                  border: "1px solid #ccc",
                  borderRadius: "3px",
                }}
              />
            </div>
            <button
              type="submit"
              style={{
                padding: "10px",
                backgroundColor: "#28a745",
                color: "white",
                border: "none",
                borderRadius: "3px",
                cursor: "pointer",
              }}
            >
              Login
            </button>
            {/* Placeholder for loading/error specific to this form */}
          </form>
        ) : (
          <div>
            <p>You are logged in.</p>
            <button
              onClick={handleFetchProfile}
              style={{
                padding: "10px",
                marginRight: "10px",
                backgroundColor: "#17a2b8",
                color: "white",
                border: "none",
                borderRadius: "3px",
                cursor: "pointer",
              }}
            >
              Fetch Profile
            </button>
            <button
              onClick={handleLogout}
              style={{
                padding: "10px",
                backgroundColor: "#dc3545",
                color: "white",
                border: "none",
                borderRadius: "3px",
                cursor: "pointer",
              }}
            >
              Logout
            </button>
            {profileData && (
              <pre
                style={{
                  marginTop: "10px",
                  backgroundColor: "#f8f9fa",
                  padding: "10px",
                  border: "1px solid #eee",
                  borderRadius: "3px",
                }}
              >
                {JSON.stringify(profileData, null, 2)}
              </pre>
            )}
            {/* Placeholder for loading/error specific to profile fetch */}
          </div>
        )}
      </section>

      {/* Password Recovery Section */}
      <section
        style={{
          border: "1px solid #ccc",
          padding: "15px",
          borderRadius: "5px",
        }}
      >
        <h2>Password Recovery</h2>

        {/* Request Reset */}
        <div style={{ marginBottom: "20px" }}>
          <h3>Request Password Reset</h3>
          <form
            onSubmit={handleRequestResetSubmit}
            style={{ display: "flex", flexDirection: "column", gap: "10px" }}
          >
            <div>
              <label htmlFor="recover-email" style={{ marginRight: "5px" }}>
                Your Email:
              </label>
              <input
                type="email"
                id="recover-email"
                // value={recoverEmail}
                // onChange={(e) => setRecoverEmail(e.target.value)}
                required
                style={{
                  padding: "8px",
                  border: "1px solid #ccc",
                  borderRadius: "3px",
                }}
              />
            </div>
            <button
              type="submit"
              style={{
                padding: "10px",
                backgroundColor: "#ffc107",
                color: "black",
                border: "none",
                borderRadius: "3px",
                cursor: "pointer",
              }}
            >
              Send Reset Link
            </button>
            {/* Placeholder for loading/error specific to this form */}
          </form>
        </div>

        {/* Confirm Reset */}
        <div>
          <h3>Confirm Password Reset</h3>
          <form
            onSubmit={handleConfirmResetSubmit}
            style={{ display: "flex", flexDirection: "column", gap: "10px" }}
          >
            <div>
              <label htmlFor="reset-token" style={{ marginRight: "5px" }}>
                Reset Token:
              </label>
              <input
                type="text"
                id="reset-token"
                placeholder="Paste token from email/URL here"
                // value={resetToken}
                // onChange={(e) => setResetToken(e.target.value)}
                required
                style={{
                  padding: "8px",
                  border: "1px solid #ccc",
                  borderRadius: "3px",
                  width: "300px",
                }}
              />
            </div>
            <div>
              <label htmlFor="reset-password" style={{ marginRight: "5px" }}>
                New Password:
              </label>
              <input
                type="password"
                id="reset-password"
                // value={resetPassword}
                // onChange={(e) => setResetPassword(e.target.value)}
                required
                style={{
                  padding: "8px",
                  border: "1px solid #ccc",
                  borderRadius: "3px",
                }}
              />
            </div>
            <button
              type="submit"
              style={{
                padding: "10px",
                backgroundColor: "#ffc107",
                color: "black",
                border: "none",
                borderRadius: "3px",
                cursor: "pointer",
              }}
            >
              Set New Password
            </button>
            {/* Placeholder for loading/error specific to this form */}
          </form>
        </div>
      </section>
    </div>
  );
};

export default AuthTestPage;
