import { useState } from "react";

export default function FilterSidebar({ onApply }) {
  const [filters, setFilters] = useState({
    genre: "",
    author: "",
    min_rating: "",
    top_k: 5,
  });

  const handleChange = (e) => {
    setFilters((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleApply = () => {
    onApply({
      ...filters,
      min_rating: filters.min_rating === "" ? null : Number(filters.min_rating),
      top_k: Number(filters.top_k),
    });
  };

  const handleClear = () => {
    const cleared = {
      genre: "",
      author: "",
      min_rating: "",
      top_k: 5,
    };
    setFilters(cleared);
    onApply({
      genre: "",
      author: "",
      min_rating: null,
      top_k: 5,
    });
  };

  return (
    <div className="sidebar">
      <h3>Filters</h3>

      <input
        type="text"
        name="genre"
        placeholder="Genre"
        value={filters.genre}
        onChange={handleChange}
      />

      <input
        type="text"
        name="author"
        placeholder="Author"
        value={filters.author}
        onChange={handleChange}
      />

      <input
        type="number"
        name="min_rating"
        placeholder="Minimum rating"
        min="0"
        max="5"
        step="0.1"
        value={filters.min_rating}
        onChange={handleChange}
      />

      <input
        type="number"
        name="top_k"
        min="1"
        max="20"
        value={filters.top_k}
        onChange={handleChange}
      />

      <button onClick={handleApply}>Apply Filters</button>
      <button className="secondary-btn" onClick={handleClear}>
        Clear
      </button>
    </div>
  );
}