import { neon } from "@neondatabase/serverless";
import React from "react";

export default async function UnsubscribePage({
  searchParams,
}: {
  searchParams: Promise<{ token?: string }>;
}) {
  const { token } = await searchParams;

  if (token) {
    const databaseUrl = process.env.NEON_DATABASE_URL;
    if (databaseUrl) {
      try {
        const sql = neon(databaseUrl);
        // Set is_subscribed to FALSE for the matching token
        await sql`
          UPDATE subscribers
          SET is_subscribed = FALSE
          WHERE unsub_token = ${token}::uuid
        `;
      } catch (error) {
        console.error("Unsubscribe error:", error);
      }
    }
  }

  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center', 
      height: '90vh',
      padding: '0 20px',
      textAlign: 'center'
    }}>
      <div style={{ maxWidth: '600px' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1.5rem', fontWeight: 'normal' }}>Unsubscribed</h1>
        <p style={{ fontSize: '1.2rem', color: '#444', lineHeight: '1.6' }}>
          You&apos;ve been unsubscribed from this service. We hope you enjoyed it nonetheless!
        </p>
        <a href="/" style={{ 
          marginTop: '2.5rem', 
          display: 'inline-block', 
          color: '#2c2c2c', 
          textDecoration: 'underline',
          fontSize: '1.1rem'
        }}>
          Return to home
        </a>
      </div>
    </div>
  );
}