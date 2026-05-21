import Navbar from "../components/Navbar";
import styles from "./about.module.css";

export default function AboutPage() {
  return (
    <>
      <Navbar />
      <main className={styles.main}>
        <h1 className={styles.title}>
          Why do this?
        </h1>
        
        <div className={styles.content}>
          <p>
            There&apos;s a curious subject in NUS College -- that&apos;s now no longer offered -- called Global Social Thought (NGT). 
            I often describe it to my friends as a political philosophy class. I didn&apos;t care much for it at the start, 
            but I first saw its relevance while listening to a lecture on Marx&apos;s Theory of Alienation: 
            Isn&apos;t this alienation from product and community why we all hate the rat race? Isn&apos;t this emptiness manifesting in China&apos;s <i>neijuan</i> and <i>tangping</i> movements?
          </p>

          <p>
            I wanted to find out more.
          </p>

          <p>
            Here&apos;s the issue: I&apos;m not trained in the social sciences. I didn&apos;t make it past many of the long, 
            dense readings. And in the times when I did, I often didn&apos;t have enough context or real-world examples 
            to intelligently critique these theories. I needed a crystal ball to show me the links between past and present.
          </p>

          <p>
            This website is my attempt at building such a crystal ball. I hope that through seeing the world 
            through the lenses of historians and political philosophers, we would collectively emerge more informed, 
            wiser and maybe even more creative in the way we frame the problems of today.
          </p>

          <p>
            Note: None of these articles are written by me. I used TinyFish to scrape the articles, and ChatGPT/Gemini
            to generate the summaries and expert opinions. 
          </p>

          <div className={styles.footer}>
            <p className={styles.footerText}>Cheers,</p>
            <p className={styles.footerText}>Timotheus</p>
            <p className={styles.footerDate}>15/5/2026</p>
          </div>
        </div>
      </main>
    </>
  );
}
