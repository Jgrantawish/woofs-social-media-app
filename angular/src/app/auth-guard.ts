import { inject } from '@angular/core';
import { CanActivateFn, RedirectCommand, Router} from '@angular/router';
import { AuthService } from './services/auth.service';
import { catchError, map, of } from 'rxjs';

export const authGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  return authService.loadSession().pipe(
    map(() => true),
    catchError(() =>
      of(
        new RedirectCommand(
          router.parseUrl('/login'),
          { replaceUrl: true }
        )
      )
    )
  );
};
