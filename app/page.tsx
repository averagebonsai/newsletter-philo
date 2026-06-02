import { Metadata } from "next";
import NewsletterPage from "./NewsletterPage";

export const metadata: Metadata = {
  alternates: {
    canonical: "/",
  },
};

export default function Page() {
  return <NewsletterPage />;
}
