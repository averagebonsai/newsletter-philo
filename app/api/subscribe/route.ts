import { neon } from "@neondatabase/serverless";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const { email } = (await request.json()) as { email?: string };

    // Validate email format and type to prevent logic injection
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || typeof email !== "string" || !emailRegex.test(email.trim())) {
      return NextResponse.json({ error: "Invalid email" }, { status: 400 });
    }

    const sanitizedEmail = email.trim().toLowerCase();

    const databaseUrl = process.env.NEON_DATABASE_URL;
    if (!databaseUrl) {
      return NextResponse.json({ error: "Database URL not configured" }, { status: 500 });
    }

    const sql = neon(databaseUrl);

    const unsubToken = crypto.randomUUID();

    // The tagged template literal automatically parameterizes the values, preventing SQL injection.
    // We use ON CONFLICT to handle re-subscriptions: if the email exists, we set is_subscribed to TRUE.
    await sql`
      INSERT INTO subscribers (email, is_subscribed, unsub_token)
      VALUES (${sanitizedEmail}, TRUE, ${unsubToken}::uuid)
      ON CONFLICT (email)
      DO UPDATE SET 
        is_subscribed = TRUE,
        unsub_token = EXCLUDED.unsub_token
    `;

    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error("Subscription error:", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}