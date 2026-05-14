"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Navbar from "../components/Navbar";

interface Newsletter {
  id: number;
  newsletterdate: string;
  title: string;
}

export default function ArchivePage() {
  const [newsletters, setNewsletters] = useState<Newsletter[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/newsletters")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        if (Array.isArray(data)) {
          setNewsletters(data);
        } else {
          console.error("Received unexpected data format:", data);
          setError("The archives are currently inaccessible.");
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch newsletters:", err);
        setError("Failed to consult the archives.");
        setLoading(false);
      });
  }, []);

  return (
    <>
      <Navbar />
      <main style={{ padding: "3rem 2rem", maxWidth: "900px", margin: "0 auto" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "2rem", borderBottom: "1px solid #2c2c2c", paddingBottom: "1rem" }}>
          Article Repository
        </h1>
        
        {loading ? (
          <p>Consulting the archives...</p>
        ) : error ? (
          <p style={{ color: "#d32f2f" }}>{error}</p>
        ) : newsletters.length === 0 ? (
          <p>The library is currently empty.</p>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
            {newsletters.map((nl) => (
              <Link key={nl.id} href={`/archive/${nl.id}`} style={{ textDecoration: "none", color: "inherit" }}>
                <div 
                  style={{ 
                    display: "flex", 
                    justifyContent: "space-between", 
                    alignItems: "center",
                    padding: "1.5rem",
                    border: "1px solid rgba(0,0,0,0.1)",
                    backgroundColor: "rgba(255,255,255,0.3)",
                    transition: "transform 0.2s, background-color 0.2s",
                    cursor: "pointer"
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.transform = "translateX(10px)";
                    e.currentTarget.style.backgroundColor = "rgba(255,255,255,0.5)";
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.transform = "translateX(0)";
                    e.currentTarget.style.backgroundColor = "rgba(255,255,255,0.3)";
                  }}
                >
                  <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                    <span style={{ fontSize: "0.8rem", textTransform: "uppercase", opacity: "0.6" }}>
                      {new Date(nl.newsletterdate).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                    </span>
                    <h2 style={{ fontSize: "1.3rem", margin: 0, fontWeight: "normal" }}>{nl.title}</h2>
                  </div>
                  <div style={{ fontSize: "1.5rem", opacity: "0.3" }}>&rarr;</div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </main>
    </>
  );
}
