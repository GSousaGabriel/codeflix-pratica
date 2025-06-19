import MovieRating from "@/app/components/movieRating"
import { render, screen } from "@testing-library/react"
import "@testing-library/jest-dom"

describe(("<movieRating />"), ()=>{
    test("renders without crashing", ()=>{
        render(<MovieRating rating="pg"/>)
        expect(screen.getByText("pg")).toBeInTheDocument()
    })

    test("renders without crashing", ()=>{
        render(<MovieRating rating="pg-13"/>)
        expect(screen.getByText("pg-13")).toBeInTheDocument()
    })
    
    test("renders without crashing", ()=>{
        render(<MovieRating rating="r"/>)
        expect(screen.getByText("r")).toBeInTheDocument()
    })
    
    test("renders without crashing", ()=>{
        render(<MovieRating rating="nc-17"/>)
        expect(screen.getByText("nc-17")).toBeInTheDocument()
    })
    
    test("renders without crashing", ()=>{
        render(<MovieRating rating="pg-1"/>)
        expect(screen.getByText("pg-1")).toBeInTheDocument()
    })

    test("renders text color accordingly to the rating 'pg'", ()=>{
        render(<MovieRating rating="pg"/>)
        expect(screen.getByText("pg")).toHaveClass('text-green-500')
    })

    test("renders text color accordingly to the rating 'pg-13'", ()=>{
        render(<MovieRating rating="pg-13"/>)
        expect(screen.getByText("pg-13")).toHaveClass('text-yellow-500')
    })
    
    test("renders text color accordingly to the rating 'r'", ()=>{
        render(<MovieRating rating="r"/>)
        expect(screen.getByText("r")).toHaveClass('text-red-500')
    })
    
    test("renders text color accordingly to the rating 'nc-17'", ()=>{
        render(<MovieRating rating="nc-17"/>)
        expect(screen.getByText("nc-17")).toHaveClass('text-purple-500')
    })
    
    test("renders text color accordingly to the rating 'pg-1'", ()=>{
        render(<MovieRating rating="pg-1"/>)
        expect(screen.getByText("pg-1")).toHaveClass('text-gray-700')
    })
})