"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import Navbar from "../../components/Navbar";

interface Newsletter {
  id: number;
  newsletterdate: string;
  title: string;
  content: string;
}

export default function ArticleView() {
  const { id } = useParams();
  const [newsletter, setNewsletter] = useState<Newsletter | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      fetch(`/api/newsletters/${id}`)
        .then((res) => {
          if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
          }
          return res.json();
        })
        .then((data) => {
          if (data && typeof data === 'object' && 'title' in data) {
            setNewsletter(data);
          } else {
            console.error("Received unexpected data format:", data);
            setError("The article is currently unreadable.");
          }
          setLoading(false);
        })
        .catch((err) => {
          console.error("Failed to fetch newsletter:", err);
          setError("Failed to consult the archives for this entry.");
          setLoading(false);
        });
    }
  }, [id]);

  if (loading) return <><Navbar /><main style={{ padding: "3rem" }}>Consulting the archives...</main></>;
  
  return (
    <>
      <Navbar />
      <article style={{ padding: "4rem 2rem", maxWidth: "800px", margin: "0 auto", lineHeight: "1.8" }}>
        <Link href="/archive" style={{ color: "#2c2c2c", fontSize: "0.9rem", textDecoration: "none", opacity: "0.6", display: "block", marginBottom: "2rem" }}>
          &larr; Back to Repository
        </Link>

        {error ? (
          <p style={{ color: "#d32f2f" }}>{error}</p>
        ) : !newsletter ? (
          <p>Article not found.</p>
        ) : (
          <>
            <header style={{ marginBottom: "3rem", borderBottom: "1px solid #2c2c2c", paddingBottom: "2rem" }}>
              <span style={{ fontSize: "0.9rem", textTransform: "uppercase", opacity: "0.6" }}>
                {new Date(newsletter.newsletterdate).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
              </span>
              <h1 style={{ fontSize: "3rem", margin: "1rem 0", fontWeight: "normal", lineHeight: "1.2" }}>{newsletter.title}</h1>
            </header>
            <div 
              style={{ fontSize: "1.1rem", whiteSpace: "pre-wrap" }}
              dangerouslySetInnerHTML={{ __html: newsletter.content.replace(/\n/g, '<br />') }}
            />
          </>
        )}
      </article>
    </>
  );
}
