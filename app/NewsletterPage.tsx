"use client";

import { useState, FormEvent } from "react";
import Navbar from "./components/Navbar";
import styles from "./page.module.css";

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
      console.warn("Subscription notice:", e.message);
      setStatus("error");
      setErrorMsg(e.message || "Something went wrong. Please try again.");
    }
  }

  return (
    <>
      <Navbar />
      <main className={styles.main}>
        <h1 className={styles.title}>
          Drawing from the Past
        </h1>
        <h3 className={styles.subtitle}>
          Incorporating the week&apos;s news with perspectives <br className={styles.tabletBreak} /> from history and political philosophy.
        </h3>

        <div className={styles.formContainer}>
          {status === "success" ? (
            <div className={styles.successMessage}>
              <p style={{ margin: 0, fontWeight: "bold" }}>
                Welcome to the fold. You&apos;ve been subscribed.
              </p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className={styles.form}>
              <input
                name="email"
                type="email"
                placeholder="Enter your email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={status === "loading"}
                className={styles.input}
              />
              <button
                type="submit"
                disabled={status === "loading"}
                className={styles.button}
              >
                {status === "loading" ? "Processing..." : "Subscribe"}
              </button>
            </form>
          )}

          {status === "error" && (
            <p className={styles.errorMessage}>
              {errorMsg}
            </p>
          )}
        </div>
      </main>
    </>
  );
}
