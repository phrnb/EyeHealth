import React, { useState } from "react";
import axios from "axios";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [token, setToken] = useState("");

  const handleRegister = async () => {
    try {
      const response = await axios.post("http://localhost:8000/register", {
        email,
        password,
      });
      setMessage(response.data.message);
    } catch (error) {
      console.error(error);
      setMessage("Error during registration.");
    }
  };

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://localhost:8000/auth", {
        email,
        password,
      });
      setToken(response.data.token);
      setMessage("Logged in successfully!");
    } catch (error) {
      console.error(error);
      setMessage("Invalid credentials.");
    }
  };

  return (
    <div>
      <h1>FastAPI + React</h1>
      <div>
        <h2>Register</h2>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleRegister}>Register</button>
      </div>

      <div>
        <h2>Login</h2>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Login</button>
      </div>

      <div>
        <h3>{message}</h3>
        {token && <p>Token: {token}</p>}
      </div>
    </div>
  );
}

export default App;