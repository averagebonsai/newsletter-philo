"use client";

import { useState, FormEvent } from "react";
import Navbar from "./components/Navbar";

export default function NewsletterPage() {
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [email, setEmail] = useState<string>("");

  const [errorMsg, setErrorMsg] = useState<string>("");

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("loading");
    setErrorMsg("");

    try {
      const response = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Subscription failed");
      }

      setStatus("success");
      setEmail("");
    } catch (e: any) {
      if (status !== "loading") { // Basic check to see if we're in a valid state
         // If it's a known error from our API, maybe just warn or log normally
      }
      console.warn("Subscription notice:", e.message);
      setStatus("error");
      setErrorMsg(e.message || "Something went wrong. Please try again.");
    }
  }

  return (
    <>
      <Navbar />
      <main
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "4rem 2rem",
          textAlign: "center",
        }}
      >
        <h1
          style={{
            fontSize: "3.5rem",
            marginBottom: "1rem",
            fontWeight: "normal",
            fontStyle: "italic",
          }}
        >
          Drawing from the Past
        </h1>
        <h3
          style={{
            fontSize: "1.2rem",
            maxWidth: "600px",
            lineHeight: "1.6",
            marginBottom: "3rem",
            fontWeight: "normal",
            opacity: "0.8",
          }}
        >
          Incorporating the week&apos;s news with perspectives from history and political philosophy.
        </h3>

        <div style={{ width: "100%", maxWidth: "500px" }}>
          {status === "success" ? (
            <div
              style={{
                padding: "1.5rem",
                border: "1px solid #2c2c2c",
                backgroundColor: "rgba(0,0,0,0.05)",
              }}
            >
              <p style={{ margin: 0, fontWeight: "bold" }}>
                Welcome to the fold. You&apos;ve been subscribed.
              </p>
            </div>
          ) : (
            <form
              onSubmit={handleSubmit}
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "1rem",
              }}
            >
              <input
                name="email"
                type="email"
                placeholder="Enter your email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={status === "loading"}
                style={{
                  padding: "1rem",
                  fontSize: "1rem",
                  backgroundColor: "transparent",
                  border: "none",
                  borderBottom: "2px solid black",
                  outline: "none",
                  fontFamily: "inherit",
                }}
              />
              <button
                type="submit"
                disabled={status === "loading"}
                style={{
                  padding: "1rem",
                  backgroundColor: "black",
                  color: "white",
                  border: "none",
                  fontSize: "1rem",
                  cursor: "pointer",
                  letterSpacing: "1px",
                  textTransform: "uppercase",
                  transition: "opacity 0.2s",
                }}
              >
                {status === "loading" ? "Processing..." : "Subscribe"}
              </button>
            </form>
          )}

          {status === "error" && (
            <p style={{ color: "#d32f2f", marginTop: "1rem" }}>
              {errorMsg}
            </p>
          )}
        </div>
      </main>
    </>
  );
}
