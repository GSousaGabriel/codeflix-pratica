const textColor = (rating: string)=>{
    switch (rating) {
        case 'pg':
            return 'text-green-500';
        case 'pg-13':
            return 'text-yellow-500';
        case 'r':
            return 'text-red-500';
        case 'nc-17':
            return 'text-purple-500';
        default:
            return 'text-gray-700';
    }
}

const MovieRating = ({ rating }: { rating: string }) => {
    return(
        <span className={`${textColor(rating)} text-xsm border-1 border-gray-700 px-2 uppercase`}>
            {rating}
        </span>
    )
}

export default MovieRating;