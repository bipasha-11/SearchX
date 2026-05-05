import React from 'react';
import { Link } from 'react-router-dom';

import { useAuth } from '../AuthContext';

function LandingPage() {
    const auth = useAuth();

    return (
        <div className="landing-hero" id="landing-page">
            <div className="landing-badge">
                <div className="landing-badge-dot"></div>
                Oracle 11g · Legal Document Intelligence
            </div>

            <h1 className="landing-title">
                Search Across Legal<br />
                Documents with <span>Precision</span>
            </h1>

            <p className="landing-description">
                SEARCHX is a DBMS-powered search engine for legal documents. Upload contracts,
                case summaries, and acts — then search across them like Ctrl+F,
                powered by an inverted index and real-time query analytics.
            </p>

            <div className="landing-actions">
                {auth.user ? (
                    <>
                        <Link to="/upload" className="btn btn-primary" id="cta-upload">
                            ⬆ Upload Document
                        </Link>
                        <Link to="/search" className="btn btn-secondary" id="cta-search">
                            🔍 Search Now
                        </Link>
                        <Link to="/analytics" className="btn btn-outline" id="cta-analytics">
                            📊 View Analytics
                        </Link>
                    </>
                ) : (
                    <Link to="/auth" className="btn btn-primary" id="cta-auth">
                        Get Started →
                    </Link>
                )}
            </div>

            <div className="landing-features">
                <div className="feature-card" id="feature-index">
                    <div className="feature-icon feature-icon-coral">📄</div>
                    <h3>Inverted Index Engine</h3>
                    <p>
                        Every uploaded document is tokenized and indexed using Oracle stored procedures.
                        Each term maps to documents with frequency-ranked relevance.
                    </p>
                </div>

                <div className="feature-card" id="feature-search">
                    <div className="feature-icon feature-icon-navy">⚖️</div>
                    <h3>Legal Domain Search</h3>
                    <p>
                        Search across contracts, case summaries, policies, acts, and legal notes.
                        Results ranked by term frequency with jurisdiction metadata.
                    </p>
                </div>

                <div className="feature-card" id="feature-analytics">
                    <div className="feature-icon feature-icon-sage">📈</div>
                    <h3>Query Analytics</h3>
                    <p>
                        Every search is logged. Track the most searched terms, search frequency trends,
                        and document indexing statistics in real-time.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default LandingPage;
