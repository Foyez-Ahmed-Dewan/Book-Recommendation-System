import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import SearchBar from "../components/Searchbar";
import FilterSidebar from "../components/FilterSidebar";
import BookGrid from "../components/BookGrid";
import {
  getProfile,
  getTrendingBooks,
  getRecentRecommendations,
  searchBooks,
} from "../api/api";

export default function Home() {
  const [profile, setProfile] = useState(null);
  const [trendingBooks, setTrendingBooks] = useState([]);
  const [recentBooks, setRecentBooks] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [activeFilters, setActiveFilters] = useState({
    genre: "",
    author: "",
    min_rating: null,
    top_k: 5,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHomePage();
  }, []);

  const loadHomePage = async () => {
    try {
      setLoading(true);

      const [profileData, trendingData, recentData] = await Promise.all([
        getProfile(),
        getTrendingBooks(),
        getRecentRecommendations(),
      ]);

      setProfile(profileData);

      const trendingList = trendingData?.results || [];
      setTrendingBooks(trendingList.slice(0, 5));

      const recentList = recentData?.results || [];
      setRecentBooks(recentList.slice(0, 5));
    } catch (error) {
      console.error("Failed to load homepage:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query) => {
    try {
      const payload = {
        query,
        top_k: activeFilters.top_k || 5,
        genre: activeFilters.genre || null,
        author: activeFilters.author || null,
        min_rating: activeFilters.min_rating,
      };

      const data = await searchBooks(payload);
      setSearchResults(data.results || []);

      const recentData = await getRecentRecommendations();
      setRecentBooks(recentData?.results || []);
    } catch (error) {
      console.error("Search failed:", error);
    }
  };

  const handleApplyFilters = (filters) => {
    setActiveFilters(filters);
  };

  if (loading) {
    return <div className="page-loading">Loading...</div>;
  }

  return (
    <div className="home-page">
      <Navbar email={profile?.email} />

      <div className="top-search-area">
        <SearchBar onSearch={handleSearch} />
      </div>

      <div className="main-layout">
        <FilterSidebar onApply={handleApplyFilters} />

        <div className="content-area">
          {searchResults.length > 0 ? (
            <BookGrid title="Search Results" books={searchResults} />
          ) : (
            <>
              <BookGrid title="Trending Books" books={trendingBooks} />
              <BookGrid
                title="Recently Recommended For You"
                books={recentBooks}
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
}