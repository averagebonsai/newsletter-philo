import Navbar from "../components/Navbar";

export default function AboutPage() {
  return (
    <>
      <Navbar />
      <main style={{ padding: "4rem 2rem", maxWidth: "800px", margin: "0 auto", lineHeight: "1.8" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1.5rem", borderBottom: "1px solid #2c2c2c", paddingBottom: "1rem", fontWeight: "normal", fontStyle: "italic" }}>
          Why do this?
        </h1>
        
        <div style={{ fontSize: "1.1rem", color: "#2c2c2c", display: "flex", flexDirection: "column", gap: "0.75rem" }}>
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

          <div style={{ marginTop: "3rem", borderTop: "1px solid rgba(0,0,0,0.1)", paddingTop: "2rem", fontStyle: "italic", opacity: "0.8" }}>
            <p style={{ margin: 0 }}>With love,</p>
            <p style={{ margin: 0 }}>Timotheus</p>
            <p style={{ margin: 0, fontSize: "0.9rem" }}>15/5/2026</p>
          </div>
        </div>
      </main>
    </>
  );
}
