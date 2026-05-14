import { neon } from "@neondatabase/serverless";
import { NextResponse } from "next/server";

export async function GET() {
  const databaseUrl = process.env.NEON_DATABASE_URL;
  if (!databaseUrl) {
    return NextResponse.json({ error: "Database URL not configured" }, { status: 500 });
  }

  try {
    const sql = neon(databaseUrl);
    const newsletters = await sql`
      SELECT id, newsletterdate, title 
      FROM newsletters 
      ORDER BY newsletterdate DESC, id DESC;
    `;
    return NextResponse.json(newsletters);
  } catch (error) {
    console.error("Fetch newsletters error:", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}
