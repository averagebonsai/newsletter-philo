import { neon } from "@neondatabase/serverless";
import { NextResponse } from "next/server";

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const databaseUrl = process.env.NEON_DATABASE_URL;
  if (!databaseUrl) {
    return NextResponse.json({ error: "Database URL not configured" }, { status: 500 });
  }

  try {
    const sql = neon(databaseUrl);
    const newsletters = await sql`
      SELECT id, newsletterdate, title, content 
      FROM newsletters 
      WHERE id = ${id};
    `;

    if (newsletters.length === 0) {
      return NextResponse.json({ error: "Newsletter not found" }, { status: 404 });
    }

    return NextResponse.json(newsletters[0], {
      headers: {
        'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
      }
    });
  } catch (error) {
    console.error("Fetch newsletter error:", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}
