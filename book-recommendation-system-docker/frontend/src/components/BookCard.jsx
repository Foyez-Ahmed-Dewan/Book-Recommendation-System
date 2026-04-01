export default function BookCard({ book }) {
  const imageSrc = book?.img ? book.img : "/placeholder.png";

  return (
    <div className="book-card">
      <img
        src={imageSrc}
        alt={book?.title || "Book"}
        onError={(e) => {
          e.currentTarget.src = "/placeholder.png";
        }}
      />
      <div className="book-card-body">
        <h4>{book?.title || "Unknown Title"}</h4>
        <p><strong>Author:</strong> {book?.author || "Unknown"}</p>
        <p><strong>Genre:</strong> {book?.genre || "N/A"}</p>
        <p><strong>Rating:</strong> {book?.rating ?? "N/A"}</p>
      </div>
    </div>
  );
}