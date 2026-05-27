import Link from "next/link";
import styles from "./Navbar.module.css";

export default function Navbar() {
  return (
    <nav className={styles.nav}>
      <Link href="/" className={styles.logo}>
        <div className={styles.logoContent}>
          <span className={styles.logoText}>
            HORIZON
          </span>
        </div>
      </Link>
      <div className={styles.links}>
        <Link href="/archive" className={styles.link}>
          Article Repository
        </Link>
        <Link href="/about" className={styles.link}>
          About
        </Link>
      </div>
    </nav>
  );
}
