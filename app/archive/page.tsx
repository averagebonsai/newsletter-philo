import { neon } from "@neondatabase/serverless";
import Link from "next/link";
import Navbar from "../components/Navbar";
import styles from "./archive.module.css";

import { Metadata } from "next";

export const metadata: Metadata = {
  alternates: {
    canonical: "/archive",
  },
};

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
      <main className={styles.main}>
        <h1 className={styles.title}>
          Article Repository
        </h1>
        
        {error ? (
          <p className={styles.error}>{error}</p>
        ) : newsletters.length === 0 ? (
          <p>The library is currently empty.</p>
        ) : (
          <div className={styles.list}>
            {newsletters.map((nl) => (
              <Link key={nl.id} href={`/archive/${nl.id}`} className={styles.itemLink}>
                <div className={styles.item}>
                  <div className={styles.itemInfo}>
                    <span className={styles.itemDate}>
                      {new Date(nl.newsletterdate).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                    </span>
                    <h2 className={styles.itemTitle}>{nl.title}</h2>
                  </div>
                  <div className={styles.itemArrow}>&rarr;</div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </main>
    </>
  );
}
