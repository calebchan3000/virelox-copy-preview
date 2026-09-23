"""Build the reviewed static copy preview from the published export.

The editable Next.js project is not in this repository. This script keeps the
existing exported layout while making the copy preview independent of stale
Next.js hydration data. Run from the repository root with beautifulsoup4.
"""

from __future__ import annotations

import hashlib
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
    css_digest = hashlib.sha256((ROOT / "copy-enhancements.css").read_bytes()).hexdigest()[:10]
    css = soup.new_tag(
        "link",
        rel="stylesheet",
        href=f"/virelox-copy-preview/copy-enhancements.css?v={css_digest}",
    )
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
    "We learned YouTube by founding and operating our own channels. Today, our researchers, writers, editors, spokespeople, and channel managers bring that experience to founders and teams with something useful to teach. Your channel is built around your voice or a named expert from your team.",
)
home.select_one("#about .partner-logos").decompose()
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
set_text(home, "#contact h2", "Start with a Free Discovery Call")
home.select_one("#contact textarea")["placeholder"] = "What should YouTube do for your brand?"
home.select_one("meta[name=description]")["content"] = (
    "Virelox Media develops educational YouTube channels for founders, experts, "
    "and companies. You record; our team researches, produces, and manages the channel."
)
home.select_one("#about .about-inner").append(
    fragment(
        home,
        """
        <aside class="founder-quote-card" aria-label="A note from Virelox Media founder Caleb Chan">
          <span class="quote-mark" aria-hidden="true">“</span>
          <blockquote>I've spent eight years building channels across finance, fitness, and other niches. Going viral is a skill: understand the audience, find the right idea, and make a video that delivers on its promise. Virelox brings that experience and our production team to your channel. Your expertise leads; we handle the work behind it.</blockquote>
          <div class="quote-attribution">
            <img src="./team/caleb-x.jpg" alt="" width="56" height="56">
            <div><strong>Caleb Chan</strong><span>Founder, Virelox Media</span></div>
          </div>
        </aside>
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
about.select_one("#how-we-work").decompose()
set_text(about, "#story .model-statement", "From one finance channel to a YouTube production team.")
story_kicker = about.select_one("#story .model-kicker")
story_statement = about.select_one("#story .model-statement")
story_heading = about.new_tag("div", attrs={"class": "story-heading"})
story_kicker.insert_before(story_heading)
story_heading.append(story_kicker.extract())
story_heading.append(story_statement.extract())
story_heading.append(
    fragment(
        about,
        """
        <figure class="about-feature">
          <img src="../team/caleb-creator-awards.jpg" alt="Caleb Chan seated with multiple YouTube Creator Awards" width="1200" height="784" loading="lazy">
          <figcaption><strong>Caleb Chan</strong><span>Founder, Virelox Media</span></figcaption>
        </figure>
        """,
    )
)
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
            <span class="story-step-number">02 / Earlier creator partnerships</span>
            <h3>Matching brands with audiences</h3>
            <p>In our earlier work through Casgains Media, we connected <strong>15+ brands</strong>, including Public.com, ExpressVPN, Interactive Brokers, and LMNT, with creators whose audiences were a natural fit for their products. Those creator partnerships represented <strong>seven figures in cumulative brand deal volume</strong> and helped brands increase conversions through relevant YouTube integrations.</p>
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
          <h3>Selected featured channels</h3>
          <p class="featured-intro">Channels we've founded and operated.</p>
          <div class="channel-logo-grid">
            <a class="channel-logo" href="https://www.youtube.com/@casgains" target="_blank" rel="noopener noreferrer" aria-label="Visit Casgains Academy on YouTube">
              <img src="../channels/casgains.jpg" alt="" width="72" height="72"><span>Casgains Academy</span><span class="channel-arrow" aria-hidden="true">↗</span>
            </a>
            <a class="channel-logo" href="https://www.youtube.com/@calebpowerlifter" target="_blank" rel="noopener noreferrer" aria-label="Visit Caleb Chan on YouTube">
              <img src="../channels/caleb.jpg" alt="" width="72" height="72"><span>Caleb Chan <small>@calebpowerlifter</small></span><span class="channel-arrow" aria-hidden="true">↗</span>
            </a>
          </div>
        </div>
        """,
    )
)
about.select_one("#founder").decompose()
set_text(
    about,
    ".cta-section .cta-inner > p:first-of-type",
    "Tell us what you know, who you want to reach, and what you hope to build on YouTube. We'll discuss the opportunity and the first videos we would consider making together.",
)
set_text(about, ".cta-section h2", "Start with a Free Discovery Call")
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
