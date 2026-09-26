import { useAuth0 } from '@auth0/auth0-react'
import { useCallback } from 'react'

// Without an API audience Auth0 issues an opaque access token that the
// backend authorizer can't verify, so we send the ID token (an RS256 JWT
// signed with the tenant's JWKS keys) as the bearer token instead.
export function useIdToken() {
  const { getAccessTokenSilently, getIdTokenClaims } = useAuth0()

  return useCallback(async () => {
    // Refreshes the session (and the cached ID token) if it has expired
    await getAccessTokenSilently()
    const claims = await getIdTokenClaims()
    return claims.__raw
  }, [getAccessTokenSilently, getIdTokenClaims])
}
