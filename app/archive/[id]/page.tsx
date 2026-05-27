import { neon } from "@neondatabase/serverless";
import Link from "next/link";
import Navbar from "../../components/Navbar";
import { notFound } from "next/navigation";

// Revalidate every 1 hour
export const revalidate = 3600;

interface Newsletter {
  id: number;
  newsletterdate: string;
  title: string;
  content: string;
}

async function getNewsletter(id: string) {
  const databaseUrl = process.env.NEON_DATABASE_URL;
  if (!databaseUrl) {
    throw new Error("Database URL not configured");
  }

  const sql = neon(databaseUrl);
  const newsletters = await sql`
    SELECT id, newsletterdate, title, content 
    FROM newsletters 
    WHERE id = ${id};
  `;

  if (newsletters.length === 0) {
    return null;
  }

  return newsletters[0] as Newsletter;
}

export default async function ArticleView({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  let newsletter: Newsletter | null = null;
  let error: string | null = null;

  try {
    newsletter = await getNewsletter(id);
  } catch (err) {
    console.error("Failed to fetch newsletter:", err);
    error = "Failed to consult the archives for this entry.";
  }

  if (!newsletter && !error) {
    notFound();
  }
  
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
