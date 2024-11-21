'use client';

import Link from 'next/link';

export default function Home() {
    return (
        <div className="page-wrapper">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-content">
                    <h1 className="hero-title">
                        Get Ready to Play on the Adversarial Playground
                    </h1>
                    <p className="hero-description">
                        Explore what happens when adversarial attacks are deployed against image classification networks and how they can be defended against!
                    </p>
                    <div className="flex flex-wrap justify-center gap-4">
                        <button className="button-primary">Get Started</button>
                        <button className="button-secondary">Learn More</button>
                    </div>
                </div>
            </section>

            {/* Content Section */}
            <section className="content-section">
                <div className="content-grid">

                    <Link href="/playground" className="block">
                        <div className="feature-card">
                            <h3 className="feature-card-title">Adversarial Playground</h3>
                            <p className="feature-card-description">
                                Play around on our playground to see the effect of adversarial attacks on image classification models!
                            </p>
                        </div>
                    </Link>

                    <Link href="/github" className="block">
                        <div className="feature-card">
                            <h3 className="feature-card-title">GitHub Page</h3>
                            <p className="feature-card-description">
                                Visit our GitHub Page!
                            </p>
                        </div>
                    </Link>

                    <Link href="/members" className="block">
                        <div className="feature-card">
                            <h3 className="feature-card-title">Team Members</h3>
                            <p className="feature-card-description">
                                Want to know more about the developers of Adversarial Playground? Click below!
                            </p>
                        </div>
                    </Link>

                    <Link href="/attacks" className="block">
                        <div className="feature-card">
                            <h3 className="feature-card-title">Attacks</h3>
                            <p className="feature-card-description">
                                Want to learn more about the attacks implemented? Click below!
                            </p>
                        </div>
                    </Link>

                </div>
            </section>
        </div>
    );
}