import { neon } from "@neondatabase/serverless";
import { NextResponse } from "next/server";

// Simple in-memory cache
let cachedNewsletters: any = null;
let lastCacheTime = 0;
const CACHE_TTL = 60 * 1000; // 60 seconds

export async function GET() {
  const databaseUrl = process.env.NEON_DATABASE_URL;
  if (!databaseUrl) {
    return NextResponse.json({ error: "Database URL not configured" }, { status: 500 });
  }

  const now = Date.now();
  if (cachedNewsletters && (now - lastCacheTime < CACHE_TTL)) {
    return NextResponse.json(cachedNewsletters, {
      headers: {
        'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=300',
        'X-Cache': 'HIT'
      }
    });
  }

  try {
    const sql = neon(databaseUrl);
    const newsletters = await sql`
      SELECT id, newsletterdate, title 
      FROM newsletters 
      ORDER BY newsletterdate DESC, id DESC;
    `;
    
    // Update cache
    cachedNewsletters = newsletters;
    lastCacheTime = now;

    return NextResponse.json(newsletters, {
      headers: {
        'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=300',
        'X-Cache': 'MISS'
      }
    });
  } catch (error) {
    console.error("Fetch newsletters error:", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}
