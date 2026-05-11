"use client";

import { useState, FormEvent } from "react";
import { neon } from "@neondatabase/serverless";

// --- SERVER ACTION (The "Backend" Logic) ---
// In Next.js, 'use server' tells the compiler this function runs safely on the server.
async function subscribeUser(email: string) {
  "use server";
  
  if (!email || !email.includes("@")) throw new Error("Invalid email");

  const databaseUrl = process.env.NEON_DATABASE_URL;
  if (!databaseUrl) throw new Error("Database URL not configured");

  const sql = neon(databaseUrl);
  
  // SAFE: The tagged template literal automatically parameterizes the input.
  // This prevents all SQL injection attacks.
  await sql`
    INSERT INTO subscribers (email, is_subscribed) 
    VALUES (${email}, TRUE)
    ON CONFLICT (email) DO UPDATE SET is_subscribed = TRUE;
  `;
}

// --- FRONTEND COMPONENT ---
export default function NewsletterPage() {
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [email, setEmail] = useState<string>("");

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("loading");

    try {
      await subscribeUser(email);
      setStatus("success");
      setEmail("");
    } catch (e) {
      console.error(e);
      setStatus("error");
    }
  }

  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: "400px" }}>
      <h2>Stay Updated</h2>
      
      {status === "success" ? (
        <p style={{ color: "green", fontWeight: "bold" }}>
          You've been subscribed, welcome!
        </p>
      ) : (
        <form onSubmit={handleSubmit} style={{ display: "flex", gap: "10px" }}>
          <input
            name="email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={status === "loading"}
            style={{ padding: "8px", flex: 1, borderRadius: "4px", border: "1px solid #ccc" }}
          />
          <button 
            type="submit" 
            disabled={status === "loading"}
            style={{ 
              padding: "8px 16px", 
              backgroundColor: "#0070f3", 
              color: "white", 
              border: "none", 
              borderRadius: "4px",
              cursor: "pointer" 
            }}
          >
            {status === "loading" ? "Joining..." : "Join"}
          </button>
        </form>
      )}

      {status === "error" && (
        <p style={{ color: "red", fontSize: "0.8rem", marginTop: "10px" }}>
          Something went wrong. Please try again.
        </p>
      )}
    </main>
  );
}