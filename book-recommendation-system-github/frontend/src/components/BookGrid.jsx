import BookCard from "./BookCard";

export default function BookGrid({ title, books }) {
  return (
    <div className="book-section">
      <h2>{title}</h2>
      <div className="book-grid">
        {books && books.length > 0 ? (
          books.map((book, index) => <BookCard key={index} book={book} />)
        ) : (
          <p>No books found.</p>
        )}
      </div>
    </div>
  );
}