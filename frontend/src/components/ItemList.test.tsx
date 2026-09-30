import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import ItemList from './ItemList'

describe('ItemList', () => {
  it('renders empty list', () => {
    const { container } = render(<ItemList items={[]} />)
    expect(container.querySelector('ul')).toBeInTheDocument()
  })
})
