import { neon } from "@neondatabase/serverless";
import Link from "next/link";
import Navbar from "../components/Navbar";

// Revalidate every 1 hour
export const revalidate = 3600;

interface Newsletter {
  id: number;
  newsletterdate: string;
  title: string;
}

async function getNewsletters() {
  const databaseUrl = process.env.NEON_DATABASE_URL;
  if (!databaseUrl) {
    throw new Error("Database URL not configured");
  }

  const sql = neon(databaseUrl);
  const newsletters = await sql`
    SELECT id, newsletterdate, title 
    FROM newsletters 
    ORDER BY newsletterdate DESC, id DESC;
  `;
  return newsletters as Newsletter[];
}

export default async function ArchivePage() {
  let newsletters: Newsletter[] = [];
  let error: string | null = null;

  try {
    newsletters = await getNewsletters();
  } catch (err) {
    console.error("Failed to fetch newsletters:", err);
    error = "Failed to consult the archives.";
  }

  return (
    <>
      <Navbar />
      <main style={{ padding: "3rem 2rem", maxWidth: "900px", margin: "0 auto" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "2rem", borderBottom: "1px solid #2c2c2c", paddingBottom: "1rem" }}>
          Article Repository
        </h1>
        
        {error ? (
          <p style={{ color: "#d32f2f" }}>{error}</p>
        ) : newsletters.length === 0 ? (
          <p>The library is currently empty.</p>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
            {newsletters.map((nl) => (
              <Link key={nl.id} href={`/archive/${nl.id}`} style={{ textDecoration: "none", color: "inherit" }}>
                <div 
                  className="archive-item"
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
      <style>{`
        .archive-item:hover {
          transform: translateX(10px);
          background-color: rgba(255,255,255,0.5) !important;
        }
      `}</style>
    </>
  );
}
