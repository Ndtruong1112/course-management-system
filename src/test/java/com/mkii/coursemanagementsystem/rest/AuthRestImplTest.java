package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.dao.IUserDao;
import com.mkii.coursemanagementsystem.dto.auth.RegisterRequest;
import com.mkii.coursemanagementsystem.entity.User;
import com.mkii.coursemanagementsystem.rest.impl.AuthRestImpl;
import com.mkii.coursemanagementsystem.security.jwt.JwtTokenProvider;
import org.junit.jupiter.api.Test;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

class AuthRestImplTest {
    @Test
    void registerNormalizesUsernameBeforeCheckingSavingAndAuthenticating() {
        IUserDao dao = mock(IUserDao.class);
        AuthenticationManager manager = mock(AuthenticationManager.class);
        PasswordEncoder encoder = mock(PasswordEncoder.class);
        JwtTokenProvider tokens = mock(JwtTokenProvider.class);
        Authentication authentication = mock(Authentication.class);
        when(encoder.encode("password")).thenReturn("encoded");
        when(dao.save(any(User.class))).thenAnswer(invocation -> invocation.getArgument(0));
        when(manager.authenticate(any())).thenReturn(authentication);
        when(tokens.generateToken(authentication)).thenReturn("token");
        AuthRestImpl controller = new AuthRestImpl(manager, dao, encoder, tokens);

        controller.register(RegisterRequest.builder().username("  alice  ").password("password").build());

        verify(dao).existsByUsername("alice");
        verify(dao).save(argThat(user -> user.getUsername().equals("alice")));
        verify(manager).authenticate(argThat(auth -> auth.getPrincipal().equals("alice")));
    }

    @Test
    void registerRejectsUsernameThatAlreadyExistsAfterNormalization() {
        IUserDao dao = mock(IUserDao.class);
        when(dao.existsByUsername(eq("alice"))).thenReturn(true);
        AuthRestImpl controller = new AuthRestImpl(mock(AuthenticationManager.class), dao,
                mock(PasswordEncoder.class), mock(JwtTokenProvider.class));

        assertThrows(BadRequestException.class, () -> controller.register(
                RegisterRequest.builder().username(" alice ").password("password").build()));
        verify(dao, never()).save(any());
    }
}
