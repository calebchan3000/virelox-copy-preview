"""Build the reviewed static copy preview from the published export.

The editable Next.js project is not in this repository. This script keeps the
existing exported layout while making the copy preview independent of stale
Next.js hydration data. Run from the repository root with beautifulsoup4.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
BASE = "3748312"


def original(path: str) -> BeautifulSoup:
    html = subprocess.check_output(
        ["git", "show", f"{BASE}:{path}"], cwd=ROOT, text=True
    )
    return BeautifulSoup(html, "html.parser")


def set_text(soup: BeautifulSoup, selector: str, value: str) -> None:
    item = soup.select_one(selector)
    assert item is not None, selector
    item.string = value


def fragment(soup: BeautifulSoup, html: str):
    return BeautifulSoup(html, "html.parser")


def finalize(soup: BeautifulSoup, path: str) -> None:
    # The published files contain multiple generations of Next.js payloads.
    # Use the existing rendered layout as a stable, self-contained preview.
    for script in soup.find_all("script"):
        script.decompose()
    for link in soup.find_all("link", attrs={"as": "script"}):
        link.decompose()
    css = soup.new_tag("link", rel="stylesheet", href="/virelox-copy-preview/copy-enhancements.css")
    soup.head.append(css)
    js = soup.new_tag("script", src="/virelox-copy-preview/copy-preview.js", defer=True)
    soup.body.append(js)
    (ROOT / path).write_text("<!doctype html>\n" + str(soup), encoding="utf-8")


home = original("index.html")
set_text(
    home,
    ".hero-sub",
    "Spend about an hour on camera each week. We research, produce, and manage educational YouTube videos built around your expertise, your voice, and organic discovery.",
)
set_text(
    home,
    ".stats-kicker",
    "Results from channels we own and operate. Client work remains confidential.",
)
set_text(home, "#about h2", "Built on our own channels. Focused on yours.")
set_text(
    home,
    "#about .about-content > p:nth-of-type(2)",
    "Virelox grew from channels we founded and operated into a team of researchers, writers, editors, spokespeople, and channel managers. Today, we bring that experience to founders, experts, and companies with something useful to teach. Client channels are built around your voice or a named expert from your team.",
)
set_text(
    home,
    ".partner-logos-label",
    "We've worked with 15+ brands, including",
)
set_text(home, "#categories .section-header > p:nth-of-type(2)", "Four stages, repeated each week. What we learn from each video informs the next one.")
steps = home.select("#categories .category-card .category-content > p:last-child")
assert len(steps) == 4
for step, copy in zip(
    steps,
    [
        "We identify the questions your audience cares about and the topics your channel can cover well. Then we develop the plan and script with your expertise at the center. If you're starting from zero, we handle channel setup and strategy too.",
        "You record one guided session a week, usually about an hour. You—or a named expert from your team—bring the ideas to life.",
        "Our editors shape each video for clarity and retention, then create a title and thumbnail that give the right audience a reason to watch. You can review the video and packaging, provide feedback, and see refinements before publication.",
        "We publish and manage the channel, then use audience response to improve the next brief. The focus is organic growth on YouTube.",
    ],
):
    step.string = copy
set_text(home, "#services .section-header h2", "For people and teams with something worth teaching")
set_text(
    home,
    "#services .section-header > p:nth-of-type(2)",
    "We work with a small number of founders, experts, and companies who want to build an educational YouTube presence without assembling an in-house production team.",
)
service_bodies = home.select("#services .service-card p")
assert len(service_bodies) == 3, len(service_bodies)
for node, copy in zip(
    service_bodies,
    [
        "Build a channel around what you know and the work you're doing, without becoming a full-time creator.",
        "Turn specialized knowledge into clear, useful videos that give people a reason to return.",
        "Develop an educational channel in your brand's voice, led by a recognizable person from your team.",
    ],
):
    node.string = copy
set_text(
    home,
    "#contact .cta-inner > p:first-of-type",
    "Tell us who you are, who you want to reach, and what you want YouTube to do for your brand. We'll review the opportunity and outline the topics, audience questions, and first videos we'd explore together.",
)
home.select_one("#contact textarea")["placeholder"] = "What should YouTube do for your brand?"
home.select_one("meta[name=description]")["content"] = (
    "Virelox Media develops educational YouTube channels for founders, experts, "
    "and companies. You record; our team researches, produces, and manages the channel."
)
home.select_one("#about .about-inner").append(
    fragment(
        home,
        """
        <div class="about-proof-card" aria-label="Caleb Chan and channels he founded or built">
          <div class="about-proof-top">
            <img class="about-proof-photo" src="./team/caleb-x.jpg" alt="Caleb Chan, founder of Virelox Media" width="320" height="320">
            <div class="about-proof-name"><strong>Caleb Chan</strong><span>Founder, Virelox Media</span></div>
          </div>
          <p>Channels built from the inside</p>
          <div class="about-proof-links">
            <a href="https://www.youtube.com/@casgains" target="_blank" rel="noopener noreferrer"><img src="./channels/casgains.jpg" alt="" width="36" height="36"><span>Casgains Academy</span><span aria-hidden="true">↗</span></a>
            <a href="https://www.youtube.com/@calebpowerlifter" target="_blank" rel="noopener noreferrer"><img src="./channels/caleb.jpg" alt="" width="36" height="36"><span>Caleb Chan</span><span aria-hidden="true">↗</span></a>
          </div>
        </div>
        """,
    )
)
finalize(home, "index.html")


about = original("about/index.html")
set_text(about, "#about-header .model-statement", "Experience built on our own channels.")
about.select_one("#about-header .model-statement").name = "h1"
about_intro = about.select("#about-header .story-copy p")
assert len(about_intro) == 2
about_intro[0].string = (
    "We began by making and growing videos ourselves. That work expanded into brand partnerships, "
    "channels across different subjects, and the production team behind Virelox."
)
about_intro[1].string = (
    "Today, we use that experience to build educational YouTube channels around our clients' expertise. "
    "You bring the knowledge and point of view; we handle the work from research through publishing."
)
highlight_bodies = about.select("#how-we-work .highlight-body")
assert len(highlight_bodies) == 4
for node, copy in zip(
    highlight_bodies,
    [
        "You record one planned session each week, typically around an hour. Our team handles the production work between sessions.",
        "Every channel has an identifiable voice: you, a founder, an educator, or a named expert from your team.",
        "We research, write, edit, and package the videos. The expertise, stories, and perspective come from you.",
        "We focus on videos people choose to find and watch, then use what we learn to improve the channel over time.",
    ],
):
    node.string = copy
set_text(about, "#story .model-statement", "From one finance channel to a YouTube production team.")
story = about.select_one("#story .story-copy")
assert story is not None
story.clear()
story.append(
    fragment(
        about,
        """
        <div class="story-steps">
          <article class="story-step">
            <span class="story-step-number">01 / Casgains Academy</span>
            <h3>Learning to earn an audience</h3>
            <p>Caleb founded <a href="https://www.youtube.com/@casgains" target="_blank" rel="noopener noreferrer">Casgains Academy</a>, where he learned to make in-depth finance and economic analysis resonate on YouTube. Its long-form videos generated <strong>more than 50 million views</strong>. He also developed a Patreon membership offering deeper stock and portfolio analysis, alongside custom tools for tracking potential investments and examining valuation metrics.</p>
          </article>
          <article class="story-step">
            <span class="story-step-number">02 / Creator partnerships</span>
            <h3>Matching brands with audiences</h3>
            <p>Through Casgains Media, we connected <strong>15+ brands</strong>, including Public.com, ExpressVPN, Interactive Brokers, and LMNT, with creators whose audiences were a natural fit for their products. Together, those partnerships represented <strong>seven figures in cumulative brand deal volume</strong> and helped brands increase conversions through relevant YouTube integrations.</p>
          </article>
          <article class="story-step">
            <span class="story-step-number">03 / Beyond finance</span>
            <h3>Building across niches</h3>
            <p>Alongside that work, Caleb built a fitness-focused channel under <a href="https://www.youtube.com/@calebpowerlifter" target="_blank" rel="noopener noreferrer">@calebpowerlifter</a>. It expanded his experience beyond finance and showed how a distinct personality and subject can shape a channel's audience.</p>
          </article>
          <article class="story-step">
            <span class="story-step-number">04 / Virelox Media</span>
            <h3>Bringing the team to your channel</h3>
            <p>That experience grew into a broader network of channels and a team of researchers, writers, editors, spokespeople, and channel managers. Virelox now brings that production experience to clients building around their own expertise.</p>
          </article>
        </div>
        """,
    )
)
story.insert_after(
    fragment(
        about,
        """
        <div class="featured-channels" id="featured-channels">
          <p class="section-kicker">Featured Channels</p>
          <h3>See the work for yourself.</h3>
          <p class="featured-intro">Public examples of channels Caleb has founded or built. They illustrate our publishing experience, not client results.</p>
          <div class="channel-grid">
            <a class="channel-card" href="https://www.youtube.com/@casgains" target="_blank" rel="noopener noreferrer" aria-label="Visit Casgains Academy on YouTube">
              <img src="../channels/casgains.jpg" alt="Casgains Academy channel avatar" width="64" height="64">
              <span class="channel-detail"><strong>Casgains Academy</strong><small>Finance &amp; economics analysis</small><span>Long-form videos with more than 50 million views, and the foundation for a paid research offering.</span><em>View channel ↗</em></span>
            </a>
            <a class="channel-card" href="https://www.youtube.com/@calebpowerlifter" target="_blank" rel="noopener noreferrer" aria-label="Visit Caleb Chan on YouTube">
              <img src="../channels/caleb.jpg" alt="Caleb Chan channel avatar" width="64" height="64">
              <span class="channel-detail"><strong>Caleb Chan <small>@calebpowerlifter</small></strong><small>Fitness &amp; creator-led content</small><span>A channel built around Caleb's interests and on-camera perspective, reaching an audience beyond finance.</span><em>View channel ↗</em></span>
            </a>
          </div>
        </div>
        """,
    )
)
founder_photo = about.select_one("#founder .founder-photo")
assert founder_photo is not None
founder_photo["src"] = "../team/caleb-x.jpg"
set_text(
    about,
    "#founder .founder-quote",
    "“I've spent eight years building channels across finance, fitness, and other niches. That work taught me that going viral takes skill: understanding an audience, finding the right idea, and making a video that delivers on its promise. We've applied those lessons repeatedly across very different subjects. Virelox brings that experience and our production team to your channel. Your expertise leads; we handle the work behind it. If we don't think we're the right fit, we'll tell you.”",
)
set_text(
    about,
    ".cta-section .cta-inner > p:first-of-type",
    "Tell us what you know, who you want to reach, and what you hope to build on YouTube. We'll discuss the opportunity and the first videos we would consider making together.",
)
about.select_one("meta[name=description]")["content"] = (
    "The story behind Virelox Media, from Casgains Academy and creator partnerships "
    "to a YouTube production team building educational channels for clients."
)
about.select_one('link[rel="icon"]')["href"] = "../favicon.png"
finalize(about, "about/index.html")

# Keep the export's alternate /about.html entry consistent with /about/.
(ROOT / "about.html").write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="robots" content="noindex,nofollow">'
    '<meta http-equiv="refresh" content="0; url=./about/">'
    '<link rel="canonical" href="./about/"></head><body>'
    '<a href="./about/">View the About page</a></body></html>\n',
    encoding="utf-8",
)
