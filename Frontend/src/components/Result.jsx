import './Results.css';

function Results({ prediction, isLoading, error }) {
  if (isLoading) {
    return <div className="results-container loading">Loading...</div>;
  }

  if (error) {
    return <div className="results-container error">Error: {error}</div>;
  }

  if (prediction) {
    return (
      <div className="results-container success">
        <p>{prediction}</p>
      </div>
    );
  }

  return <div className="results-container initial">The result will appear here.</div>;
}

export default Results;