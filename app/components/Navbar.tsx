import Link from "next/link";

export default function Navbar() {
  return (
    <nav
      style={{
        backgroundColor: "black",
        color: "white",
        padding: "1rem 2rem",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <Link href="/" style={{ textDecoration: "none", color: "white" }}>
        <div style={{ display: "flex", flexDirection: "column", lineHeight: "1" }}>
          <span style={{ fontSize: "1.2rem", fontWeight: "bold", letterSpacing: "1px" }}>
            TROUILLOT'S
          </span>
          <span style={{ fontSize: "0.8rem", textTransform: "uppercase", opacity: "0.8" }}>
            Crystal Ball
          </span>
        </div>
      </Link>
      <div style={{ display: "flex", gap: "2rem" }}>
        <Link href="/archive" style={{ color: "white", textDecoration: "none", fontSize: "0.9rem", fontWeight: "500" }}>
          Article Repository
        </Link>
        <Link href="#" style={{ color: "white", textDecoration: "none", fontSize: "0.9rem", fontWeight: "500" }}>
          About
        </Link>
      </div>
    </nav>
  );
}
