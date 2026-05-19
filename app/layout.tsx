import type { Metadata } from "next";
import Script from "next/script";

export const metadata: Metadata = {
  title: "Horizon",
  description: "A newsletter blending current affairs with history and political philosophy.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        style={{
          margin: 0,
          padding: 0,
          backgroundColor: "#f4f1ea", // Parchment color
          color: "#2c2c2c",
          fontFamily: "'Georgia', serif",
          minHeight: "100vh",
        }}
      >
        <Script
          async
          src="https://www.googletagmanager.com/gtag/js?id=G-VVC5QGGHWJ"
        />
        <Script id="google-analytics">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-VVC5QGGHWJ');
          `}
        </Script>
        {children}
      </body>
    </html>
  );
}
