import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const token = request.cookies.get('token')?.value;
    const { pathname } = request.nextUrl;

    // Public routes that don't require auth
    const publicRoutes = ['/', '/login', '/register'];

    // Check if the current path is a protected route
    // Protected routes are anything NOT in publicRoutes (and not static files)
    const isPublicRoute = publicRoutes.includes(pathname);
    const isStaticAsset = pathname.startsWith('/_next') || pathname.includes('.');

    if (isStaticAsset) {
        return NextResponse.next();
    }

    // Redirect to login if accessing protected route without token
    if (!isPublicRoute && !token) {
        const url = request.nextUrl.clone();
        url.pathname = '/login';
        return NextResponse.redirect(url);
    }

    // Redirect to dashboard if accessing public route (like login) WITH token
    if (isPublicRoute && token && pathname !== '/') {
        const url = request.nextUrl.clone();
        url.pathname = '/dashboard';
        return NextResponse.redirect(url);
    }

    return NextResponse.next();
}

export const config = {
    matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
